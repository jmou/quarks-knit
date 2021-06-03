import matplotlib.pyplot as plt


def viz1(img, img_th, img_cleaned):
    f, ax = plt.subplots(1, 3, figsize=(20, 14))

    ax[0].imshow(img, cmap='gray')
    ax[0].axis('off')
    ax[0].set_title('Model perdiction')

    ax[1].imshow(img_th, cmap='gray')
    ax[1].axis('off')
    ax[1].set_title('Threshhold image')

    ax[2].imshow(img_cleaned, cmap='gray')
    ax[2].axis('off')
    ax[2].set_title('Cleaned image')

    f.savefig('fig1.jpg')
    return
